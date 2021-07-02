(function () {
  console.log('JS is loaded');

  const questionForm = document.querySelector('#questionForm')
  questionForm.addEventListener('submit', function (event) {
    console.log('form submitted with value:', questionForm.questionInput.value)
    event.preventDefault()
  })
})();
