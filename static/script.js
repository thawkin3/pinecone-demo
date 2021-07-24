(() => {
  const sanitizeHTML = (str) => str.replace(/[^\w. ]/gi, (c) => '&#' + c.charCodeAt(0) + ';');

  const questionForm = document.querySelector('#questionForm')
  const resultsContainer = document.querySelector('#resultsContainer')
  const resultsHeader = document.querySelector('#resultsHeader')
  const resultsTableBody = document.querySelector('#resultsTableBody')

  questionForm.addEventListener('submit', event => {
    event.preventDefault()

    resultsContainer.style.display = 'none'

    const sanitizedUserInput = sanitizeHTML(questionForm.question.value)

    resultsHeader.innerHTML = `Search results for <a href="https://www.quora.com/search?q=${sanitizedUserInput}" target="_blank" rel="noopener noreferrer">your question</a>:`

    fetch(`/api/search?question=${sanitizedUserInput}`)
      .then(response => response.json())
      .then(data => {
        const tableBodyContent = data.reduce((output, item) => {
          output += `<tr><td class="questionColumn">${item.question}</td><td class="scoreColumn">${(item.score * 100).toFixed(2)}%</td></tr>`
          return output
        }, '')

        resultsTableBody.innerHTML = tableBodyContent
        resultsContainer.style.display = 'block'
      })
      .catch(() => {
        alert('Whoops! Something went wrong while searching.')
      })
  })
})()
