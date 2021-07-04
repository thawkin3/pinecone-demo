(() => {
  const questionForm = document.querySelector('#questionForm')
  const resultsContainer = document.querySelector('#resultsContainer')
  const resultsTableBody = document.querySelector('#resultsTableBody')

  questionForm.addEventListener('submit', event => {
    event.preventDefault()

    resultsContainer.style.display = "none"

    fetch(`/api/search?question=${questionForm.question.value}`)
      .then(response => response.json())
      .then(data => {
        const tableBodyContent = data.reduce((output, item) => {
          output += `<tr><td class="questionColumn">${item.question}</td><td class="scoreColumn">${(item.score * 100).toFixed(2)}%</td></tr>`
          return output
        }, '')

        resultsTableBody.innerHTML = tableBodyContent
        resultsContainer.style.display = "block"
      })
  })
})()
