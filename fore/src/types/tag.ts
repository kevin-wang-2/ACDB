import { MergeOptional } from "@/utils/mergeObject";

interface BaseTagModel {
  name: string;
  category: string;
}

export interface TagModel<T extends PropertyType> extends BaseTagModel {
  property: T;
}

export interface DummyProperty {}

export interface LengthProperty {
  length: number;
}

export interface SocketProperty {
  socket: number;
}

export type SubmitTagModel = MergeOptional<
  MergeOptional<BaseTagModel, LengthProperty>,
  SocketProperty
>;

export type PropertyType = DummyProperty | LengthProperty | SocketProperty;
