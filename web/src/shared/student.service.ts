import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { Student, Score, ExamResult } from './models';
import { BaseService } from './base-service';

@Injectable({
  providedIn: 'root'
}) 
export class StudentService extends BaseService {
  protected override baseUrl = '/api/student'; // 使用代理URL

  constructor(http: HttpClient) {
    super(http);
  }

  getStudentProfile(studentId: string): Observable<Student> {
    return this.getOne<Student>(`profile/${studentId}`);
  }

  getStudentScores(studentId: string): Observable<Score[]> {
    // 根据后端返回示例：API 返回 { data: [ { 学生姓名, 成绩, 成绩编号, 科目, 考试类型 }, ... ], message, success, timestamp }
    // 使用 BaseService.getList 解析包装后的 response.data，然后把中文字段映射到 Score 接口
    return this.getList<any>(`scores/chinese/${studentId}`)
      .pipe(
        map(items => items.map(item => ({
          score_id: Number(item['成绩编号']),
          score: Number(item['成绩']),
          exam_name: item['考试类型'],
          subject_name: item['科目'],
          student_name: item['学生姓名']
        } as Score)))
      );
  }

  getStudentExamResults(studentId: string): Observable<ExamResult[]> {
    return this.getJsonWithFallback<ExamResult>(`exam_results/${studentId}`)
      .pipe(
        // 转换字符串类型字段为数字类型
        map(data => data.map(item => 
          this.transformObjectFields<ExamResult>(item, [
            'chinese', 'math', 'english', 'physics', 'chemistry', 'politics', 'total_score', 'ranking'
          ])
        ))
      );
  }
}