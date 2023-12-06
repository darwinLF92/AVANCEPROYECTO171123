document.addEventListener('DOMContentLoaded', function () {
    var modals = document.querySelectorAll('.modal');
    M.Modal.init(modals);

    var errorModal = document.getElementById('modalError');
    if (errorModal) {
      var errorInstance = M.Modal.getInstance(errorModal);
      errorInstance.open();
    }

    var successModal = document.getElementById('modalSuccess');
    if (successModal) {
      var successInstance = M.Modal.getInstance(successModal);
      successInstance.open();
    }
  });