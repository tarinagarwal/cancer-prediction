
$(document).ready(function() {
  // Step navigation
  $('#nextBtn').on('click', function() {
    $('#step1').hide();
    $('#step2').show();
  });


  $('#ageInput').on('input', function() {
    $('#ageSlider').val(this.value);
  });
  $('#ageSlider').on('input', function() {
    $('#ageInput').val(this.value);
  });
});
