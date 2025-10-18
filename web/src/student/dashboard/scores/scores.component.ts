import { Component, Input } from '@angular/core';
import { Score } from '../../../shared/models';
import { NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-scores',
  standalone: true,
  imports: [NgIf, NgFor],
  template: `
    <div class="section">
      <h3>成绩列表</h3>
      <table class="data-table" *ngIf="scores.length > 0">
        <thead>
          <tr>
            <th>科目</th>
            <th>考试类型</th>
            <th>分数</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let score of scores">
            <td>{{score.subject_name}}</td>
            <td>{{score.exam_name}}</td>
            <td>{{score.score}}</td>
          </tr>
        </tbody>
      </table>
      <p *ngIf="scores.length === 0 && !loading">暂无成绩记录</p>
      <p *ngIf="loading">加载中...</p>
    </div>
  `,
  styles: [`
    .section {
      margin-bottom: 30px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      padding: 20px;
    }

    .section h3 {
      margin-top: 0;
      color: #333;
      border-bottom: 2px solid #3f51b5;
      padding-bottom: 10px;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }

    .data-table th,
    .data-table td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }

    .data-table th {
      background-color: #f5f5f5;
      font-weight: bold;
      color: #333;
    }

    .data-table tbody tr:hover {
      background-color: #f9f9f9;
    }

    .data-table tbody tr:last-child td {
      border-bottom: none;
    }
  `]
})
export class ScoresComponent {
  @Input() scores: Score[] = [];
  @Input() loading: boolean = false;
}