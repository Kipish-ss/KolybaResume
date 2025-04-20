import { NewUser } from "./new-user";

export interface UpdateUser extends NewUser {
    id: number;
}