
(function validaGit() {
  console.log("ENTRO EN JS");
  var direccion=document.getElementById("dirGitHub").value;
  var at=document.getElementById("email").value;  
  if (direccion.length==0) {
     alert("Es obligatorio indicar un nombre");
     console.log("no esta vacia");
     return false;
  }  
  console.log(direccion);  
  start = direccion.split(":");
  console.log(start.length); 
  if (start.length>1){  
      console.log("Empieza por http");  
      direccion = direccion.split("/");
      if (direccion[1] != "github.com"){
         console.log(direccion[1]);
         alert("Error");
         return false
      }
      if (direccion.length != 5){
         console.log(direccion.length +" "+ direccion[1]);   
         alert("URL incorrecta");
         return false  
      }
  }  
  start = direccion.split(".");
  if (start.length>1){  
      console.log("Empieza por www");
      direccion = direccion.split("/");
      if (direccion[0] != "www.github.com"){
         console.log(direccion[2]);
         alert("Error");
         return false
      }
      if (direccion.length != 3){
         console.log(direccion.length +" "+ direccion[1]);   
         alert("URL incorrecta");
         return false  
      }
  }else{
    alert("URL incorrecta"); 
  }

  expr = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  if (at.length == 0){
      alert("La dirección de email no puede estar vacia");
      return false     
  }else if ( !expr.test(at)){
      alert("Error: La dirección de correo " + at + " es incorrecta.");
      return false    
  }
});   

