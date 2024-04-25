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
  
    $("#submitQuestions").click(function () {
        var issuesList = [];
        $("#issuesTable tbody tr").each(function () {
            var problem = $(this).find('textarea').first().val();
            var solution = $(this).find('textarea').last().val();
            if (problem && solution) {
                issuesList.push({ problem: problem, solution: solution });
            }
        });
  
        var allData = {
            companyContext: $("#companyContext").val(),
            botInfo: $("#botInfo").val(),
            botGoals: $("#botGoals").val(),
            issues: issuesList,
            botLang: $("#botLang").val(),
        };
  
        $.ajax({
            type: "POST",
            url: "/questions",
            contentType: "application/json",
            data: JSON.stringify(allData),
            success: function () {
                console.log("Context updated successfully.");
                window.location.href = "/bots";
            },
            error: function () {
                console.error("Failed to update context.");
            }
        });
    });})