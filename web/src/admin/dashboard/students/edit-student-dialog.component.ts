import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { CommonModule } from '@angular/common';
import { AdminService } from '../../../shared/admin.service';
import { Student, Class } from '../../../shared/models';

@Component({
  selector: 'app-edit-student-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule
  ],
  template: `
    <h2 mat-dialog-title>编辑学生</h2>
    <mat-dialog-content>
      <form [formGroup]="studentForm" (ngSubmit)="onSubmit()">
        <mat-form-field appearance="fill" class="full-width">
          <mat-label>学生ID</mat-label>
          <input matInput formControlName="student_id" [disabled]="true">
        </mat-form-field>
        
        <mat-form-field appearance="fill" class="full-width">
          <mat-label>学生姓名</mat-label>
          <input matInput formControlName="student_name" required>
          <mat-error *ngIf="studentForm.get('student_name')?.invalid && studentForm.get('student_name')?.touched">
            学生姓名是必填项
          </mat-error>
        </mat-form-field>
        
        <mat-form-field appearance="fill" class="full-width">
          <mat-label>班级</mat-label>
          <mat-select formControlName="class_id" required>
            <mat-option *ngFor="let class of classes" [value]="class.class_id">
              {{class.class_name}}
            </mat-option>
          </mat-select>
          <mat-error *ngIf="studentForm.get('class_id')?.invalid && studentForm.get('class_id')?.touched">
            班级是必选项
          </mat-error>
        </mat-form-field>
      </form>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button (click)="onCancel()">取消</button>
      <button mat-raised-button color="primary" (click)="onSubmit()" [disabled]="studentForm.invalid">
        保存
      </button>
    </mat-dialog-actions>
  `,
  styles: [`
    .full-width {
      width: 100%;
      margin-bottom: 16px;
    }
  `]
})
export class EditStudentDialogComponent implements OnInit {
  studentForm: FormGroup;
  classes: Class[] = [];

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<EditStudentDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { student: Student },
    private adminService: AdminService
  ) {
    this.studentForm = this.fb.group({
      student_id: [data.student.student_id, Validators.required],
      student_name: [data.student.student_name, Validators.required],
      class_id: [data.student.class_id, Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadClasses();
  }

  loadClasses(): void {
    this.adminService.getClasses().subscribe({
      next: (classes) => {
        this.classes = classes;
        // 设置表单的class_id默认值
        if (this.data.student.class_name) {
          const matchedClass = classes.find(c => c.class_name === this.data.student.class_name);
          if (matchedClass) {
            this.studentForm.patchValue({ class_id: matchedClass.class_id });
          }
        }
      },
      error: (error) => {
        console.error('加载班级数据失败:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.studentForm.valid) {
      const formValue = this.studentForm.getRawValue();
      const selectedClass = this.classes.find(c => c.class_id === formValue.class_id);
      
      const studentUpdate: any = {
        student_id: formValue.student_id,
        student_name: formValue.student_name,
        class_id: formValue.class_id
      };
      
      if (selectedClass) {
        studentUpdate.class_name = selectedClass.class_name;
      }
      
      this.dialogRef.close(studentUpdate);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}