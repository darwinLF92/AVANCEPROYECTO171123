document.addEventListener('DOMContentLoaded', function () {
  // Mostrar el modal de error si existe
  var errorModal = document.getElementById('modalError');
  if (errorModal) {
    Swal.fire({
      title: 'Error',
      text: errorModal.querySelector('p').textContent,
      icon: 'error',
    });
  }

  // Mostrar el modal de éxito si existe
  var successModal = document.getElementById('modalSuccess');
  if (successModal) {
    Swal.fire({
      title: 'Éxito',
      text: successModal.querySelector('p').textContent,
      icon: 'success',
    });
  }
});
