import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { FileUploadModule } from 'primeng/fileupload';

import { InputTextModule } from 'primeng/inputtext';
import { TextareaModule } from 'primeng/textarea';
import { ResumeUploadService } from '../../services/resume-upload.service';
import { log } from 'node:console';
import { AnalyzeResponse, ResumeResult } from '../../models/results';

@Component({
  selector: 'app-resume-upload',
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule,
    FileUploadModule,
    TextareaModule,
    InputTextModule,
  ],
  templateUrl: './resume-upload.html',
  styleUrl: './resume-upload.scss',
})
export class ResumeUpload {
  jobDescription = '';
  skills = '';
  selectedFile: any;

 result:ResumeResult[] = [];



  selectedFiles: File[] = [];

constructor(private resumeService: ResumeUploadService) {}
  

 onSelectFiles(event: any) {
  this.resumeService.setFiles(event.files);
const files: File[] = event.currentFiles;
  console.log("Uploaded files:", files);

    files.forEach((file, index) => {
    console.log(`File ${index + 1}:`);
    console.log('Name:', file.name);
    console.log('Type:', file.type);
    console.log('Size:', file.size);
    this.selectedFiles.push(file);
  });

  // Optional check
  if (event.files.length > 0) {
    alert(`${event.files.length} file(s) selected`);
  }
}
 analyze() {


  console.log("Files from service:", this.selectedFiles);

  if (!this.selectedFiles || this.selectedFiles.length === 0) {
    alert("Please upload resumes first!");
    return;
  }

this.resumeService
  .uploadResumes(this.jobDescription, this.skills, this.selectedFiles)
  .subscribe((res: AnalyzeResponse) => {
    this.result = res.results;
    console.log("Analysis result:", this.result);
  });

}

}
