export interface ResumeResult {
  filename: string;
  file_type: string;
  ats_score: number;
  matched: string[];
  missing: string[];
}
export interface AnalyzeResponse {
  results: ResumeResult[];
}
