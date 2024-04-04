
   $(document).ready(function () {
// delete course or unit
// Attach the event listener to a parent element that exists on page load (e.g., document)
document.addEventListener('click', function(event) {
  // Check if the clicked element has the class 'deletecourse'
  if (event.target && event.target.classList.contains('deleteitem')) {
      event.preventDefault(); // Prevent the default behavior of the link

      var url = event.target.getAttribute('data-url');
      let name = event.target.getAttribute('data-name')
      
      // Show a confirmation dialog using Bootbox
      bootbox.confirm({
          message: `Are you sure you want to delete ${name}`,
          buttons: {
              confirm: {
                  label: 'Yes',
                  className: 'btn-danger'
              },
              cancel: {
                  label: 'No',
                  className: 'btn-secondary'
              }
          },
          callback: function(result) {
              // If user confirms deletion, redirect to delete URL
              if (result) {
                  window.location.href = url;
              }
          }
      });
  }
});





    // Add a click event listener to the delete button
    document.querySelectorAll('.deleteuser').forEach(function(button) {
      button.addEventListener('click', function() {
          var userurl = this.getAttribute('data-url');
          
          // Show a confirmation dialog using Bootbox
          bootbox.confirm({
              message: "Are you sure you want to delete this user?",
              buttons: {
                  confirm: {
                      label: 'Yes',
                      className: 'btn-danger'
                  },
                  cancel: {
                      label: 'No',
                      className: 'btn-secondary'
                  }
              },
              callback: function(result) {
                  // If user confirms deletion, redirect to delete URL
                  if (result) {
                      window.location.href = userurl;
                  }
              }
          });
      });
  });

    
    // edit usertype
    var userType =document.getElementById('usertypeedit');

    if (userType){

      userType = userType.value
    console.log(userType)
    var courseField = document.getElementById('courseField');

    if ( userType === '2'|| userType === '3') {
        courseField.style.display = 'block';
    } else {
        courseField.style.display = 'none';
    }
  }

    // Get the score input element
    function calculateTotal() {
      var lab = parseInt(document.getElementById('lab').value) || 0;
      var quiz = parseInt(document.getElementById('quiz').value) || 0;
      var endsem = parseInt(document.getElementById('endsem').value) || 0;
      var midsem = parseInt(document.getElementById('midsem').value) || 0;
    

      var total = lab + quiz + endsem + midsem;
      document.getElementById('total_score').value = total;
  }

  // Call calculateTotal() function whenever any input field changes
  var scoreInput = document.getElementById('total_score');
if (scoreInput) {
  document.querySelectorAll('input[type="number"]').forEach(item => {
      item.addEventListener('input', calculateTotal);
  });

  // Initial calculation when the page loads
  calculateTotal();
}
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


      // display student marks
      $("#user-student").change(function(e){
        e.preventDefault()
        var studentId = $(this).val();
        var url = $("#user-student").attr("data-course-url");  
  
        $.ajax({                     
          url: url,                   
          data: {
            'studentid': studentId      
          },
          success: function (data) {  
           
            $("#displaymarks").html(data);  
          }
        });
  
      })
      // display student report
      $("#user-studentreport").change(function(e){
        e.preventDefault()
        var studentId = $(this).val();
        var url = $("#user-studentreport").attr("data-course-url");  
  
        $.ajax({                     
          url: url,                   
          data: {
            'studentid': studentId      
          },
          success: function (data) {  
           
            $("#displayreport").html(data);  
          }
        });
  
      })
      //select student course
      $("#student").change(function(e){
        e.preventDefault()
        var studentId = $(this).val();
        var url = $("#student").attr("data-course-url");  
  
        $.ajax({                     
          url: url,                   
          data: {
            'studentid': studentId      
          },
          success: function (data) {   
            $("#unitnames").html(data);  
          }
        });
  
      })

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

       