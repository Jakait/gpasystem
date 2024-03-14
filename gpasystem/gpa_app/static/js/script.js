   // Add this script to your HTML file
   $(document).ready(function () {
    // this an element for fetching units and course using ajax on document reload

    courselement = document.getElementById("id_course");
     if (courselement) {
      var courseId = $("#id_course").val();
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

    }

     // Check if an element with the specified ID exists
     let element = document.getElementById("idaccess");
     if (element) {
          var accessId = $("#idaccess").val();
          var url = $("#registrationuserForm").attr("data-course-url");  
    
          $.ajax({                     
            url: url,                   
            data: {
              'access': accessId      
            },
            success: function (data) {   
              $("#addcourses").html(data);  
            }
          });
    
        
     }

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

      //view courses and units
      $("#id_courseview").change(function (e) {
       
        e.preventDefault()
        var courseId = $(this).val();
        var url = $("#id_courseview").attr("data-course-url");  
  
        $.ajax({                     
          url: url,                   
          data: {
            'course': courseId      
          },
          success: function (data) {   
            $("#tableviewcourse").html(data);  
          }
        });
  
      });

      $("#idaccess").change(function (e) {
       
        e.preventDefault()
        var accessId = $(this).val();
        var url = $("#registrationuserForm").attr("data-course-url");  
  
        $.ajax({                     
          url: url,                   
          data: {
            'access': accessId      
          },
          success: function (data) {   
            $("#addcourses").html(data);  
          }
        });
  
      });



});

       