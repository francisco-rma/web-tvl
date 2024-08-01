import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { TasksService } from '../services/tasks.services';
import { AsyncPipe } from '@angular/common';
import { NgFor } from '@angular/common';
import { Observable } from 'rxjs';
import { MenuComponent } from "../menu/menu.component";

@Component({
  selector: 'app-tasks',
  standalone: true,
  imports: [RouterModule, AsyncPipe, NgFor, MenuComponent],
  templateUrl: './tasks.component.html',
  styleUrl: './tasks.component.css'
})

export class TasksComponent implements OnInit {
  constructor(private tasksService: TasksService) {
  }

  tasks$: Observable<any> | undefined;

  ngOnInit() {
    this.tasks$ = this.tasksService.listTasks();
  }

  listTasks() {
    this.tasksService.listTasks().subscribe((data) => {
      console.log(data);
    });
  }
}
