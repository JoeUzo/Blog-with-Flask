 function toggleCommentBox(id) {
   var commentBox = document.getElementById(id);
   var addCommentBtn = document.getElementById('addCommentBtn' + id.replace( /^\D+/g, ''));
   if (commentBox.style.display == 'none') {
     commentBox.style.display = 'block';
     ClassicEditor.create(document.querySelector('#editor' + id.replace( /^\D+/g, '')));
   } else {
     commentBox.style.display = 'none';
     addCommentBtn.style.display = 'block';
   }
 }

 function confirmDelete() {
   return confirm('Are you sure you want to delete this post?');
 }

