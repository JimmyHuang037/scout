import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base-service';

@Injectable({
  providedIn: 'root'
})
export class AdminService extends BaseService {
  protected override baseUrl = '/api/admin';

  constructor(http: HttpClient) {
    super(http);
  }

  // 可以在这里添加管理员相关的API调用方法
}
