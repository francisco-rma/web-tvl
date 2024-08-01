import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({ providedIn: 'root' })
export class TasksService {
    constructor(private http: HttpClient) {
    }

    listTasks() {
        return this.http.get('http://localhost/api/v1/tasks/list-tasks');
    }
}
