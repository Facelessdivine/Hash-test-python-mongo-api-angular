import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent implements OnInit {

  user = {
    username: '',
    password: ''
  }
  response = ''
  show = false
  

  constructor(private authService: AuthService,
              private router: Router          
    ) {
      if (authService.getToken() != null){
        this.router.navigate(['/private-tasks']);
      } 
     }

  ngOnInit() {
  }
  
  signIn(){
    this.authService.signIn(this.user)
    .subscribe( res => {
      // console.log(res);
      if(res.message == "Login failed"){
      this.response= res.response
      this.show = true
      } else {
        localStorage.setItem('token', res.token);
        this.router.navigate(['/private-tasks']);
      }
    })
  }

}
