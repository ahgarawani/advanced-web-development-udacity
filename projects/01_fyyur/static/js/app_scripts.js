document.addEventListener('DOMContentLoaded', function() {
  btn = document.getElementById('del-btn');
  if (btn){
    btn.onclick = function(e) {
      const item_data = e.target.dataset;
      fetch('/' + item_data['type'] + '/' + item_data['id'], {
        method: 'DELETE'
      });
    };
  }
});