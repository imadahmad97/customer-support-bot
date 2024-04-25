$(document).ready(function () {
  $("#initialQuestionsModal").modal("show");

  // Initially show only the first question and hide others
  $(".question").hide(); // Hide all questions
  $("#question1").show(); // Show only the first question

  // Handle clicking on the "Add Row" button
  $("#addRow").click(function () {
      var newRow = '<tr contenteditable="true"><td><textarea class="form-control"></textarea></td><td><textarea class="form-control"></textarea></td></tr>';
      $("#issuesTable tbody").append(newRow);
  });

  // Handle clicking on the "Next" button
  $(".next-btn").click(function () {
      var currentQuestion = $(this).closest(".question");
      var nextQuestion = currentQuestion.next(".question");

      currentQuestion.hide();
      if (nextQuestion.length) {
          nextQuestion.show();
      } else {
          $("#submitQuestions").show();
      }
  });

  // Handle clicking on the "Submit Questions" button
  $("#submitQuestions").click(function () {
      var allData = {
          companyContext: $("#companyContext").val(),
          botInfo: $("#botInfo").val(),
          botGoals: $("#botGoals").val(),
          issues: issuesList,
          botLang: $("#botLang").val(),
      };

      $.ajax({
          type: "POST",
          url: "/setContext",
          contentType: "application/json",
          data: JSON.stringify(allData),
          success: function () {
              console.log("Context updated successfully.");
              $("#initialQuestionsModal").modal("hide");
          },
          error: function () {
              console.error("Failed to update context.");
          }
      });
  });

});


  $("#messageArea").on("submit", function (event) {
    event.preventDefault();
    const date = new Date();
    const hour = date.getHours();
    const minute = date.getMinutes();
    const str_time = hour + ":" + minute;
    var rawText = $("#text").val();

    var userHtml =
      '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' +
      rawText +
      '<span class="msg_time_send">' +
      str_time +
      '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';
    $("#text").val("");
    $("#messageFormeight").append(userHtml);

    $.ajax({
      data: JSON.stringify({ msg: rawText }),
      contentType: "application/json",
      type: "POST",
      url: "/get",
    }).done(function (data) {
      var botText = data.response;
      var botHtml =
        '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' +
        botText +
        '<span class="msg_time">' +
        str_time +
        "</span></div></div>";
      $("#messageFormeight").append($.parseHTML(botHtml));
    });
  });