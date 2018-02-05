command: "/usr/local/bin/python2 /Users/mattbramlage/uebersicht_scripts/tasks_assigned_to_me.py"

refreshFrequency: 5 * 1000 * 60

style: """
  bottom: 30px
  left: 20px
  color: #fff
  font-family: Helvetica Neue


  table
    border-collapse: collapse
    table-layout: fixed

  .wrapper
    padding: 4px 6px 4px 6px
    position: relative

  #user p
    font-weight: bold

  .taskname
    background: rgba(#fff, 0.2)

  .duedate
    background: rgba(#fff, 0.1)

  p
    padding: 0
    margin: 0
    font-size: 11px
    font-weight: normal
    max-width: 100%
    color: #ddd
    text-overflow: ellipsis
    text-shadow: none

  #errors
    font-weight: bold
    color: #F99
    font-size: 40px

"""


render: -> """
  <div id='user'>
    <p>Fetching data...</p>
  <table>
    <tr id='results'>
      <td class='taskname'></td>
      <td class='duedate'></td>
    </tr>
  </table>
  <div id='errors'>
  </div>
"""

update: (output, domEl) ->
  data = JSON.parse(output)
  results = data['results']

  resultsel = $(domEl).find('#user')
  resultsel.html "<p>Focus tasks for #{results['user']['name']} <img src=\"#{results['user']['pic']}\"></img>:</p>"

  resultsel = $(domEl).find('#results')
  resultsel.html "<p>Focus tasks for #{results[0]}:</p>"

  errors = data['errors']
  errorel = $(domEl).find('#errors')
  errorel.html "<p>#{errors}</p>"

