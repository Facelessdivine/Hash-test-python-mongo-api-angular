import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  user = {
    username: '',
    password: ''
  }
  
  response = '';
  show= false;

  constructor(private authService: AuthService,
  private router: Router
  ) { 
    if (authService.getToken() != null){
      this.router.navigate(['/private-tasks']);
    } 
  }

  ngOnInit() {

  }
  signUp(){
    this.authService.signUp(this.user)
    .subscribe( res => {
      // console.log(res);
      if(res.alert){
      this.response= res.alert
      this.show = true
      } else {
        localStorage.setItem('token', res.token);
        this.router.navigate(['/private-tasks']);
      }
    })
  }

}
