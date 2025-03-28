import { reactive } from 'vue'

interface Course {
  course_code: string;
  day: string;
  time_start: string;
  time_end: string;
  location: string;
}

export const store = reactive({
  courses: [],
  issues: [],
  
  // Schedule analyzer state
  fallSchedule: null as File | null,
  winterSchedule: null as File | null,
  loading: false,
  analysisResult: null as { 
    courses: Course[], 
    cs_requirements: string[] 
  } | null,
  
  // Computed-like getters
  get canAnalyze() {
    return this.fallSchedule && this.winterSchedule;
  },
  
  // Methods
  setFallSchedule(file: File) {
    this.fallSchedule = file;
  },
  
  setWinterSchedule(file: File) {
    this.winterSchedule = file;
  },
  
  async analyzeSchedules() {
    this.loading = true;
    
    try {
      // Create FormData object to send files
      const formData = new FormData();
      
      if (this.fallSchedule) {
        formData.append('file1', this.fallSchedule);
      }
      
      if (this.winterSchedule) {
        formData.append('file2', this.winterSchedule);
      }
      
      // Use the correct endpoint from the backend
      const isProd: boolean = import.meta.env.VITE_DEV == 'false';
    
    
    let endpoint;
      if (isProd){
        endpoint = import.meta.env.VITE_PROD_URL;
      } else {
        endpoint = import.meta.env.VITE_DEV_URL
      }
      endpoint+='/api/upload';
      alert(endpoint)
    
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header - browser will set it with boundary for FormData
      });
      
      if (!response.ok) {
        console.error('API Error:', response.status, response.statusText);
        throw new Error(`Failed to fetch data: ${response.status} ${response.statusText}`);
      }
      
      const data = await response.json();
      this.analysisResult = data;
      
    } catch (error) {
      console.error('Error analyzing schedules:', error);
      throw error;
    } finally {
      this.loading = false;
    }
    
    return this.analysisResult;
  },
  
  resetState() {
    this.fallSchedule = null;
    this.winterSchedule = null;
    this.analysisResult = null;
    this.loading = false;
  }
})
