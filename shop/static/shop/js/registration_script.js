$('.popup-bg').click(function (e) {
    if (!$(e.target).closest(".popup").length) {
      $('.popup-bg').fadeOut(600);
    }
  });