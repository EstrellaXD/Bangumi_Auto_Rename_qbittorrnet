export interface LoginSuccess {
  access_token: string;
  token_type: string;
  expire: number;
}

export interface Update extends LoginSuccess {
  message: 'update success';
}

export interface User {
  username: string;
  password: string;
}
