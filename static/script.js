(function () {
  console.log('JS is loaded');

  const questionForm = document.querySelector('#questionForm')
  const resultsContainer = document.querySelector('#resultsContainer')
  const resultsTableBody = document.querySelector('#resultsTableBody')

  questionForm.addEventListener('submit', function (event) {
    console.log('form submitted with value:', questionForm.question.value)
    event.preventDefault()

    resultsContainer.style.display = "none"

    fetch(`/api/search?question=${questionForm.question.value}`)
      .then(response => response.json())
      .then(data => {
        console.log(data)

        const tableBodyContent = data.reduce((output, item) => {
          output += `<tr><td class="questionColumn">${item.question}</td><td class="scoreColumn">${item.score.toFixed(2)}</td></tr>`
          return output
        }, '')

        resultsTableBody.innerHTML = tableBodyContent
        resultsContainer.style.display = "block"
      });
  })
})();
