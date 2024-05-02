$(document).ready(function () {
    // Modal and Questions UI Interaction
    $("#initialQuestionsModal").modal("show");
  
    $(".question").hide();
    $("#question1").show();
  
    $("#addRow").click(function () {
        var newRow = '<tr contenteditable="true"><td><textarea class="form-control"></textarea></td><td><textarea class="form-control"></textarea></td></tr>';
        $("#issuesTable tbody").append(newRow);
    });
  
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
    });