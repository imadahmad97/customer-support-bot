function sendInitialContext(botId, context) {
  $.ajax({
      type: "POST",
      url: `/get/${botId}`,
      contentType: "application/json",
      data: JSON.stringify({ msg: context }),
      success: function (data) {
          var botText = data.response;
          var date = new Date();
          var str_time = date.getHours() + ":" + date.getMinutes();
          var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/nbjZnHd/chatbot.png" class="rounded-circle user_img_msg"></div><div class="msg_container">' + botText + '<span class="msg_time">' + str_time + "</span></div></div>";
          $("#messageFormeight").append($.parseHTML(botHtml));
      },
      error: function (error) {
          console.error("Failed to fetch initial context response:", error);
      }
  });
}


$(document).ready(function () {
  var botId = $('#botId').data('id');
  if(botId && botContext) {
      sendInitialContext(botId, botContext);
  }
  $("#messageArea").on("submit", function (event) {
      event.preventDefault();
      const botId = $('#botId').data('id');  
      const date = new Date();
      const hour = date.getHours();
      const minute = date.getMinutes();
      const str_time = hour + ":" + minute;
      const rawText = $("#text").val();

      var userHtml =
          '<div class="d-flex justify-content-end mb-4"><div class="msg_container_send">' +
          rawText +
          '<span class="msg_time_send">' +
          str_time +
          '</span></div><div class="img_cont_msg"><img src="https://iili.io/JgELtiF.png" class="rounded-circle user_img_msg"></div></div>';
      $("#text").val("");
      $("#messageFormeight").append(userHtml);

      $.ajax({
          data: JSON.stringify({ msg: rawText }),
          contentType: "application/json",
          type: "POST",
          url: `/get/${botId}`,
          success: function (data) {
              var botText = data.response;
              var botHtml =
                  '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/nbjZnHd/chatbot.png" class="rounded-circle user_img_msg"></div><div class="msg_container">' +
                  botText +
                  '<span class="msg_time">' +
                  str_time +
                  "</span></div></div>";
              $("#messageFormeight").append($.parseHTML(botHtml));
          },
          error: function (error) {
              console.error("Failed to fetch response:", error);
          }
      });
  });
});
