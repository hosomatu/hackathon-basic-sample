export type EnvName = 'dev' | 'prod';

export interface Region {
  region: string;
}
export const DefaultRegion: Region = {
  region: 'ap-northeast-1'
};

export interface StackParameter {
  envName: EnvName;
  vpcCidr: string;
}
export const DevStackParameter: StackParameter = {
  envName: 'dev',
  vpcCidr: "10.1.0.0/16",
};