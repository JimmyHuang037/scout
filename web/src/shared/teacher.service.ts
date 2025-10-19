import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base-service';

@Injectable({
  providedIn: 'root'
})
export class TeacherService extends BaseService {
  protected override baseUrl = '/api/teacher'; // 使用代理URL

  constructor(http: HttpClient) {
    super(http);
  }

  // 可以在这里添加教师相关的API调用方法
}