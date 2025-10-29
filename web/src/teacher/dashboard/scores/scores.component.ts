import { Component, Input, ViewChild, AfterViewInit, OnDestroy } from '@angular/core';
import { StudentScore } from '../../../shared/models';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator';
import { MatSortModule, MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-scores',
  standalone: true,
  imports: [
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatCardModule,
    MatProgressSpinnerModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    CommonModule
  ],
  template: `
    <mat-card class="scores-card">
      <mat-card-header>
        <mat-card-title>成绩管理</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        @if (loading) {
          <div class="loading-container">
            <mat-spinner diameter="30"></mat-spinner>
            <span>加载中...</span>
          </div>
        } @else {
          <div class="scores-table-container">
            <mat-form-field class="search-field">
              <mat-label>搜索</mat-label>
              <input matInput (keyup)="applyFilter($event)" placeholder="输入关键词进行搜索" #input>
            </mat-form-field>
            
            <table mat-table [dataSource]="dataSource" matSort>
              <!-- 学生ID列 -->
              <ng-container matColumnDef="student_id">
                <th mat-header-cell *matHeaderCellDef mat-sort-header>学生ID</th>
                <td mat-cell *matCellDef="let element">{{element.student_id}}</td>
              </ng-container>

              <!-- 学生姓名列 -->
              <ng-container matColumnDef="student_name">
                <th mat-header-cell *matHeaderCellDef mat-sort-header>学生姓名</th>
                <td mat-cell *matCellDef="let element">{{element.student_name}}</td>
              </ng-container>

              <!-- 科目列 -->
              <ng-container matColumnDef="subject_name">
                <th mat-header-cell *matHeaderCellDef mat-sort-header>科目</th>
                <td mat-cell *matCellDef="let element">{{element.subject_name}}</td>
              </ng-container>

              <!-- 分数列 -->
              <ng-container matColumnDef="score">
                <th mat-header-cell *matHeaderCellDef mat-sort-header>分数</th>
                <td mat-cell *matCellDef="let element">{{element.score}}</td>
              </ng-container>

              <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
              <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
            </table>

            <mat-paginator 
              [pageSizeOptions]="[5, 10, 20]" 
              showFirstLastButtons 
              aria-label="选择页面">
            </mat-paginator>
          </div>
        }
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .scores-card {
      margin-bottom: 16px;
    }
    .loading-container {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      gap: 10px;
    }
    .search-field {
      width: 100%;
      margin-bottom: 16px;
    }
    .scores-table-container {
      overflow-x: auto;
    }
    table {
      width: 100%;
    }
    .mat-mdc-table .mat-mdc-row:hover {
      background-color: #f5f5f5;
    }
  `]
})
export class ScoresComponent implements AfterViewInit, OnDestroy {
  @Input() loading: boolean = false;
  @Input() set scores(scores: StudentScore[]) {
    this.dataSource.data = scores || [];
  }

  displayedColumns: string[] = ['student_id', 'student_name', 'subject_name', 'score'];
  dataSource = new MatTableDataSource<StudentScore>();

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnDestroy() {
    // Clean up data source to prevent memory leaks
    this.dataSource.disconnect();
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}