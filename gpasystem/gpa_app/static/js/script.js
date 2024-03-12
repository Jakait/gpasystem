   // Add this script to your HTML file
   jQuery(document).ready(function () {
    // Toggle active class for the clicked link and collapse other submenus
    $('.list-group-item').on('click', function () {
        $('.list-group-item').removeClass('active');
        $(this).addClass('active');

        // Collapse other submenus
        $('.collapse.show').removeClass('show');
    });

    // Highlight the active link on page load
    var path = window.location.pathname;
    $('.list-group-item').removeClass('active');
    $('.list-group-item[href="' + path + '"]').addClass('active');

    $("#id_course").change(function (e) {
        e.preventDefault()
        var courseId = $(this).val();
        var url = $("#id_course").attr("data-course-url");  
  
        $.ajax({                     
          url: url,                   
          data: {
            'course': courseId      
          },
          success: function (data) {   
            $("#courseupdate").html(data);  
          }
        });
  
      });



});

       