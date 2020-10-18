import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Private_taks_service } from '../../services/private-taks.service';


@Component({
  selector: 'app-private-tasks',
  templateUrl: './private-tasks.component.html',
  styleUrls: ['./private-tasks.component.css']
})
export class PrivateTasksComponent implements OnInit {

  constructor(public auth:AuthService, private taskService: Private_taks_service ) {

   }
   
  user = {
    id: '',
    username: ''
    
  } 
  keys = {
    public_key: '',
    private_key: '',
  }

  show = false;
  showkeypv = false;
  showkeypb = false;
  method = '';
  response = '';

  ngOnInit() {
    this.getUsers()
  }

  
  deleteUsers(usuario){
    if (confirm('¿Estás Seguro que deseas eliminar a este usuario? ') == true) {
    this.taskService.DeleteUser(usuario).subscribe(res =>{
      this.method = 'Deleted'
      this.show=true;
      this.response = usuario
      // console.log(JSON.stringify(res))
    });
    this.getUsers();
    setTimeout(() => {
      this.show=false;
      this.getUsers();
  }, 5000);
    }
  }
  
  update(usuario: string){
    let input = prompt(`Introduce el nuevo nombre de usuario`);
    this.user.id = usuario
    this.user.username = input;
    this.taskService.Update(this.user).subscribe(res => {
      this.method = 'Updated'
      this.show=true;
      this.response = this.user.username
      // console.log(JSON.stringify(res))
    });
    this.getUsers();
    setTimeout(() => {
      this.show=false;
      this.getUsers();
    }, 5000);
  }


  getKeys(id: any) {
    let s = this.taskService.selectUserKeys
    let resp = this.taskService.getKeys(id);
    resp.subscribe( res => {
      s = res;
      this.keys.private_key = s.private_key
      this.keys.public_key = s.public_key
      // this.showkeys = true;
    })
  }
  getUsers() {
    let resp = this.auth.getUsers();
    resp.subscribe((res) => {
      this.auth.DatosUser = res;
    })
  }

}
