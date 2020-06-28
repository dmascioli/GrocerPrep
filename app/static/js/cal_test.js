function addCalendar() {
    document.addEventListener('DOMContentLoaded', function () {
        var calendarEl = document.getElementById('calendar');
        var Draggable = FullCalendar.Draggable;

        var containerEl = document.getElementById("draggables");
        var draggableEl = document.getElementById("draggables");

        var calendar = new FullCalendar.Calendar(calendarEl, {
            headerToolbar: {
                left: 'prevYear,prev,next,nextYear today',
                center: 'title',
                right: 'dayGridMonth,dayGridWeek,listWeek'
            },
            initialDate: '2020-06-12',
            droppable: true,
            drop: function(info) {
                
            },
            aspectRatio: 1.75,
            navLinks: true, // can click day/week names to navigate views
            editable: true,
            dayMaxEvents: true, // allow "more" link when too many events
            events: [
                {
                    title: 'All Day Event',
                    start: '2020-06-01'
                },
                {
                    title: 'Long Event',
                    start: '2020-06-07',
                    end: '2020-06-10'
                },
                {
                    groupId: 999,
                    title: 'Repeating Event',
                    start: '2020-06-09T16:00:00'
                },
                {
                    groupId: 999,
                    title: 'Repeating Event',
                    start: '2020-06-16T16:00:00'
                },
                {
                    title: 'Conference',
                    start: '2020-06-11',
                    end: '2020-06-13'
                },
                {
                    title: 'Meeting',
                    start: '2020-06-12T10:30:00',
                    end: '2020-06-12T12:30:00'
                },
                {
                    title: 'Lunch',
                    start: '2020-06-12T12:00:00'
                },
                {
                    title: 'Meeting',
                    start: '2020-06-12T14:30:00'
                },
                {
                    title: 'Happy Hour',
                    start: '2020-06-12T17:30:00'
                },
                {
                    title: 'Dinner',
                    start: '2020-06-12T20:00:00'
                },
                {
                    title: 'Birthday Party',
                    start: '2020-06-13T07:00:00'
                },
                {
                    title: 'Click for Google',
                    url: 'http://google.com/',
                    start: '2020-06-28'
                }
            ]
        });

        calendar.render();

        new Draggable(containerEl, {
            itemSelector: '.recipe',
            eventData: function(eventEl) {
                return {
                  title: eventEl.innerText
                };
              }
          });
        
    });
}
