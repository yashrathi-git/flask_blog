tinymce.init({
    selector: 'textarea',
    height: 500,
    menubar: false,
    plugins: [
      'advlist autolink lists link image charmap print preview anchor paste',
      'searchreplace visualblocks fullscreen',
      'media table paste help wordcount codesample'
    ],
    mobile: { 
      theme: 'mobile' 
    },
    toolbar: 'media image link | undo redo |  formatselect | bold italic backcolor  | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | codesample | fullscreen help',
    content_css: [
      '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
    ],
    paste_as_text: true,
    branding:false,
    help_tabs:['shortcuts'],
    placeholder:'Start typing your post. Click help icon to see some useful shortcuts.'
  });