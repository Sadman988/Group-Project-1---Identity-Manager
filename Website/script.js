document.getElementById('downloadBtn').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default download action

    var userAgreement = confirm("I agree to download the file.");
    if (userAgreement) {
      // If user agrees, trigger the download
      window.location.href = this.href;
    }
  });