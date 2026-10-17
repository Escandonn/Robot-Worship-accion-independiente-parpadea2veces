export interface FaceComponent {
  name: string;
  type: string;
  data: string;
}

export interface FaceResponse {
  success: boolean;
  components: FaceComponent[];
}
