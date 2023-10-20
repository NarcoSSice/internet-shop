$('.auth-form-bg').click(function (e) {
    if (!$(e.target).closest(".auth-form").length) {
      $('.auth-form-bg').fadeOut(600);
    }
  });