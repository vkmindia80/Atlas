/// <reference types="react-scripts" />

declare module 'react-beautiful-dnd' {
  import { Component, ReactElement, ReactNode } from 'react';

  export interface DragDropContextProps {
    onDragStart?: (result: any) => void;
    onDragEnd: (result: any) => void;
    children: ReactNode;
  }

  export interface DroppableProps {
    droppableId: string;
    children: (provided: any, snapshot: any) => ReactElement;
  }

  export interface DraggableProps {
    draggableId: string;
    index: number;
    children: (provided: any, snapshot: any) => ReactElement;
  }

  export const DragDropContext: React.FC<DragDropContextProps>;
  export const Droppable: React.FC<DroppableProps>;
  export const Draggable: React.FC<DraggableProps>;
}