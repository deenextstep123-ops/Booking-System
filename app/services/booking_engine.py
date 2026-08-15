from app.models.booking import Booking, BookingStatus
from app.models.unavailable_period import UnavailablePeriod
from app.models.working_hours import WorkingHours

from datetime import datetime, timedelta


#  Found a great use for AI - generates very clean comments. very useful

# datetime.combine() answers when exactly? timedelta says how much time?

class BookingEngine:

    def is_within_working_hours(self, staff, requested_start, requested_end):
        """
        Checks whether a requested booking fits completely inside one of the
        staff member's working periods for that day.

        Returns:
            True  - the whole booking fits inside a working period
            False - it does not
        """

        # requested_start is a datetime object.
        # datetime.weekday() gives us:
        # 0 = Monday, 1 = Tuesday ... 6 = Sunday.
        #
        # This matches the integers we store in WorkingHours.day_of_week.
        weekday = requested_start.weekday()

        # Query the WorkingHours table for rows where:
        # 1. staff_id matches the Staff object passed into this method
        # 2. day_of_week matches the requested booking's weekday
        #
        # .all() executes the query and returns a list of WorkingHours objects.
        working_hours = WorkingHours.query.filter(
            WorkingHours.staff_id == staff.id,
            WorkingHours.day_of_week == weekday
        ).all()

        # There may be multiple working periods on the same day.
        # Example:
        # 09:00 - 12:00
        # 13:00 - 17:00
        for work in working_hours:

            # requested_start and requested_end are datetime objects,
            # while work.start_time and work.end_time are time objects.
            #
            # .time() extracts only the clock-time part from a datetime.
            #
            # The whole requested booking must fit inside this working period.
            if (
                requested_start.time() >= work.start_time
                and requested_end.time() <= work.end_time
            ):
                return True

        # If none of the working periods contain the whole booking,
        # the requested time is outside working hours.
        return False


    def overlaps_unavailable_period(self, staff, requested_start, requested_end):
        """
        Checks whether a requested booking overlaps a period that the admin
        has manually marked as unavailable.

        Returns:
            True  - there is an overlap
            False - there is no overlap
        """

        # Get all manually blocked periods belonging to this staff member.
        unavailable_periods = UnavailablePeriod.query.filter(
            UnavailablePeriod.staff_id == staff.id
        ).all()

        for period in unavailable_periods:

            # Two time ranges overlap when:
            #
            # requested_start < existing_end
            # AND
            # requested_end > existing_start
            #
            # Both conditions are necessary.
            #
            # Example:
            #
            # blocked:      13:00 -------- 15:00
            # requested:          14:00 -------- 16:00
            #
            # 14:00 < 15:00  -> True
            # 16:00 > 13:00  -> True
            #
            # Therefore they overlap.
            if (
                requested_start < period.end_time
                and requested_end > period.start_time
            ):
                return True

        return False


    def overlaps_existing_booking(self, staff, requested_start, requested_end):
        """
        Checks whether the requested booking overlaps an existing booking.

        Only CONFIRMED and PENDING bookings block a time slot.
        CANCELLED bookings should not prevent somebody else booking the slot.

        Returns:
            True  - requested time clashes with an existing booking
            False - there is no clash
        """

        # Find bookings belonging to this staff member whose status is
        # either CONFIRMED or PENDING.
        #
        # .in_() is SQLAlchemy's equivalent of asking:
        #
        # status IN (confirmed, pending)
        existing_bookings = Booking.query.filter(
            Booking.staff_id == staff.id,
            Booking.status.in_([
                BookingStatus.CONFIRMED,
                BookingStatus.PENDING
            ])
        ).all()

        for booking in existing_bookings:

            # Use the same general overlap rule as UnavailablePeriod.
            if (
                requested_start < booking.end_time
                and requested_end > booking.start_time
            ):
                return True

        return False


    def is_available(self, staff, requested_start, requested_end):
        """
        Combines all of the individual availability rules.

        A booking is available only when:
        1. It is completely inside working hours.
        2. It does not overlap an unavailable period.
        3. It does not overlap a pending/confirmed booking.

        Returns:
            True  - the requested booking can be made
            False - something prevents the booking
        """

        # First check normal working hours.
        if not self.is_within_working_hours(
            staff,
            requested_start,
            requested_end
        ):
            return False

        # Then check admin-created blocked periods.
        if self.overlaps_unavailable_period(
            staff,
            requested_start,
            requested_end
        ):
            return False

        # Finally check existing bookings.
        if self.overlaps_existing_booking(
            staff,
            requested_start,
            requested_end
        ):
            return False

        # None of the rules rejected the requested time,
        # therefore the booking is available.
        return True


    def get_available_slots(self, staff, service, requested_date):
        """
        Generates all available booking start times for a particular date.

        Possible start times are generated every 15 minutes.

        The Service object's duration_minutes determines how long each
        candidate booking would last.

        Example:
            Service duration = 30 minutes

            Candidate starts:
            09:00 -> candidate booking is 09:00-09:30
            09:15 -> candidate booking is 09:15-09:45
            09:30 -> candidate booking is 09:30-10:00
            etc.

        Only candidates that pass is_available() are returned.
        """

        # We will append valid datetime objects to this list.
        available_slots = []

        # requested_date is a Python date object.
        #
        # .weekday() gives us the corresponding day number:
        # Monday = 0 ... Sunday = 6.
        weekday = requested_date.weekday()

        # Find all working periods for this staff member on this weekday.
        working_hours = WorkingHours.query.filter(
            WorkingHours.staff_id == staff.id,
            WorkingHours.day_of_week == weekday
        ).all()

        # A day can contain multiple working periods.
        #
        # Example:
        # 09:00 - 12:00
        # 13:00 - 17:00
        for work in working_hours:

            # work.start_time is only a TIME:
            #
            #     09:00
            #
            # requested_date is only a DATE:
            #
            #     2026-08-17
            #
            # datetime.combine() joins those two pieces together:
            #
            #     date        + time
            #     2026-08-17  + 09:00
            #
            # becomes:
            #
            #     datetime
            #     2026-08-17 09:00
            #
            # This gives us an exact point in time that the booking engine
            # can work with.
            current_time = datetime.combine(
                requested_date,
                work.start_time
            )

            # Do the same with the end of this working period.
            #
            # Example:
            #
            # requested_date = 2026-08-17
            # work.end_time  = 17:00
            #
            # working_end becomes:
            # 2026-08-17 17:00
            working_end = datetime.combine(
                requested_date,
                work.end_time
            )

            # Start at the beginning of this working period and repeatedly
            # generate possible booking start times.
            while current_time < working_end:

                # timedelta represents a DURATION rather than an exact
                # date/time.
                #
                # service.duration_minutes is an integer, for example:
                #
                #     30
                #
                # We cannot directly do:
                #
                #     datetime + 30
                #
                # because Python does not know whether 30 means seconds,
                # minutes, hours, etc.
                #
                # timedelta(minutes=30) explicitly creates a duration of
                # thirty minutes.
                #
                # Example:
                #
                # current_time = 09:00
                # service.duration_minutes = 30
                #
                # candidate_end:
                # 09:00 + 30 minutes = 09:30
                candidate_end = current_time + timedelta(
                    minutes=service.duration_minutes
                )

                # Pass this candidate booking through all of the
                # availability rules we've already written.
                if self.is_available(
                    staff,
                    current_time,
                    candidate_end
                ):
                    # We only need to save the start time.
                    # The end time can always be calculated from the
                    # service duration.
                    available_slots.append(current_time)

                # Move to the next possible booking start.
                #
                # Again, timedelta represents an amount of time.
                #
                # Example:
                #
                # 09:00 + 15 minutes = 09:15
                # 09:15 + 15 minutes = 09:30
                # 09:30 + 15 minutes = 09:45
                #
                # This is what produces our 15-minute booking increments.
                current_time += timedelta(minutes=15)

        # After every working period has been checked, return all of the
        # valid candidate start times.
        return available_slots