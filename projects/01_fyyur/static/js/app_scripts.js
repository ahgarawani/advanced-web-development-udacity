document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('del-btn');
  if (btn){
    btn.onclick = function(e) {
      const item_data = e.target.dataset;
      fetch('/' + item_data['type'] + '/' + item_data['id'], {
        method: 'DELETE',
        redirect: 'follow',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(function(response) {
        document.location.href = response.url;
      });
    };
  }
});