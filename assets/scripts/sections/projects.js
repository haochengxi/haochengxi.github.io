// Keep filtered cards in normal grid flow so every row stays aligned.
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.projects-section').forEach((section) => {
    const buttons = section.querySelectorAll('.project-filtr-control')
    const cards = section.querySelectorAll('.project-card')

    buttons.forEach((button) => {
      button.addEventListener('click', () => {
        const filter = button.dataset.filter
        cards.forEach((card) => {
          const categories = card.dataset.category.split(',')
          card.hidden = filter !== 'all' && !categories.includes(filter)
        })
        buttons.forEach((control) => {
          const selected = control === button
          control.classList.toggle('active', selected)
          control.setAttribute('aria-pressed', String(selected))
        })
      })
    })
  })
})
