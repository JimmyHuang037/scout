import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
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
    return this.getList<Score>(`scores/${studentId}`);
  }

  getStudentExamResults(studentId: string): Observable<ExamResult[]> {
    return this.getJsonWithFallback<ExamResult>(`exam_results/${studentId}`)
      .pipe(
        // 转换字符串类型字段为数字类型
        map(data => data.map(item => this.transformExamResult(item)))
      );
  }

  private transformExamResult(item: any): ExamResult {
    return {
      exam_name: item.exam_name,
      student_name: item.student_name,
      chinese: this.transformToNumber(item.chinese),
      math: this.transformToNumber(item.math),
      english: this.transformToNumber(item.english),
      physics: this.transformToNumber(item.physics),
      chemistry: this.transformToNumber(item.chemistry),
      politics: this.transformToNumber(item.politics),
      total_score: this.transformToNumber(item.total_score),
      ranking: this.transformToNumber(item.ranking)
    };
  }
}