jQuery(document).ready(function(){
    jQuery('.datetimepicker').datepicker({
        dateFormat: 'mm/dd/yy',
        timepicker: true,
      });
    jQuery("#add-event").submit(function(){
        var values = {};
        $.each($('#add-event').serializeArray(), function(i, field) {
            values[field.name] = field.value;
        });
        console.log(
          values
        );
    });
  });
  
  (function () {    
      'use strict';
      // ------------------------------------------------------- //
      // Calendar
      // ------------------------------------------------------ //
      jQuery(function() {
          // page is ready
          jQuery('#calendar').fullCalendar({
              themeSystem: 'bootstrap4',
              // emphasizes business hours
              businessHours: false,
              defaultView: 'month',
              // event dragging & resizing
              editable: true,
              // header
              header: {
                  left: 'title',
                  center: 'month,agendaWeek,agendaDay',
                  right: 'today prev,next'
              },
              events: tasks,
              eventRender: function(event, element) {
                  if(event.icon){
                      element.find(".fc-title").prepend("<i class='fa fa-"+event.icon+"'></i>");
                  }
                },
              dayClick: function() {
                  jQuery('#modal-view-event-add').modal();
              },
              eventClick: function(event, jsEvent, view) {
                      jQuery('.event-icon').html("<i class='fa fa-"+event.icon+"'></i>");
                      jQuery('.event-title').html(event.title);
                      jQuery('.event-body').html(event.description);
                      jQuery('.eventUrl').attr('href',event.url);
                      jQuery('#modal-view-event').modal();
              },
          })
      });
    
  })(jQuery);