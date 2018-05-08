type WasmHeap = DataView;

export abstract class CType {
  // Base class for all CTypes
}

interface CTypeClass<U> {
  // Interface describing the CType CLASS OBJECTS.
  // Specifically for every CType class, we statically know
  // its size, and how to build it from the heap.
  sizeof(): number;
  from_heap(heap: WasmHeap, off: number): U;
}

export class Void implements CType {
  static sizeof(): number {
    throw new Error("void doesn't have a size");
  }
  static from_heap(heap: WasmHeap, off: number): Void {
    throw new Error("void can't be instantiated");
  }
  constructor() {}
}

abstract class NumberCType implements CType {
  protected _val: number;
  abstract min(): number;
  abstract max(): number;

  constructor(arg: number) {
    assert (arg >= this.min() && arg <= this.max());
    this._val = arg;
  }
  val(): number { return this._val; };
}

function assert(b: boolean): void {
  if (!b) {
    throw new Error("assert");
  }
}

export class Uint8 extends NumberCType {
  min(): number { return 0 };
  max(): number { return (1<<8-1); };
  static sizeof(): number { return 8 };
  static from_heap(heap: WasmHeap, off: number): Uint8
  {
    return new Uint8(heap.getUint8(off));
  }
}

export class Sint8 extends NumberCType {
  min(): number { return -(1<<7); };
  max(): number { return (1<<7)-1; };
  static sizeof(): number { return 8 };
  static from_heap(heap: WasmHeap, off: number): Sint8
  {
    return new Sint8(heap.getInt8(off));
  }
}

export class Uint16 extends NumberCType {
  min(): number { return 0 };
  max(): number { return (1<<16-1); };
  static sizeof(): number { return 16 };
  static from_heap(heap: WasmHeap, off: number): Uint16
  {
    return new Uint16(heap.getUint16(off));
  }
}

export class Sint16 extends NumberCType {
  min(): number { return -(1<<15); };
  max(): number { return (1<<15)-1; };
  static sizeof(): number { return 16 };
  static from_heap(heap: WasmHeap, off: number): Sint16
  {
    return new Sint16(heap.getInt16(off));
  }
}

export class Uint32 extends NumberCType {
  min(): number { return 0 };
  max(): number { return (1<<32-1); };
  static sizeof(): number { return 32 };
  static from_heap(heap: WasmHeap, off: number): Uint32
  {
    return new Uint32(heap.getUint32(off));
  }
}

export class Sint32 extends NumberCType {
  sizeof(): number { return 32 };
  min(): number { return -(1<<31); };
  max(): number { return (1<<31)-1; };
  static sizeof(): number { return 32 };
  static from_heap(heap: WasmHeap, off: number): Sint32
  {
    return new Sint32(heap.getInt32(off));
  }
}

export class Uint64 extends NumberCType {
  min(): number { return 0 };
  max(): number { return (1<<64-1); };
  static sizeof(): number { return 64 };
  static from_heap(heap: WasmHeap, off: number): Uint64
  {
    throw "64 bit numbers NYI";
  }
}

export class Sint64 extends NumberCType {
  sizeof(): number { return 64 };
  min(): number { return -(1<<31); };
  max(): number { return (1<<31)-1; };
  static sizeof(): number { return 64 };
  static from_heap(heap: WasmHeap, off: number): Sint64
  {
    throw "64 bit numbers NYI";
  }
}

export class Float extends NumberCType {
  sizeof(): number { return 32 };
  min(): number { return -(1<<31); };
  max(): number { return (1<<31)-1; };
  static sizeof(): number { return 32 };
  static from_heap(heap: WasmHeap, off: number): Float 
  {
    return new Float(heap.getFloat32(off));
  }
}

export class Double extends NumberCType {
  sizeof(): number { return 64 };
  min(): number { return -(1<<31); };
  max(): number { return (1<<31)-1; };
  static sizeof(): number { return 64 };
  static from_heap(heap: WasmHeap, off: number): Double
  {
    return new Double(heap.getFloat64(off));
  }
}

export class Ptr<U extends CType> extends Uint32 {
  private _heap: WasmHeap;
  private _typ: CTypeClass<U>;

  constructor(arg: number, heap: WasmHeap, typ: CTypeClass<U>) {
    super(arg);
    this._heap = heap;
    this._typ = typ;
  }

  deref(): U {
    return this._typ.from_heap(this._heap, this._val);
  }

  index(idx: number): this {
    let new_addr = this._val + idx * this._typ.sizeof();
    return this.constructor(new_addr, this._heap, this._typ);
  }

  heap(): WasmHeap {
    return this._heap;
  }

  static nullPtr<T extends CType>(typ: CTypeClass<T>, heap?: WasmHeap): Ptr<T> {
    if (heap === undefined) {
      heap = null;
    }

    return new Ptr<T>(0, heap, typ);
  }
}

export class CString extends Ptr<Uint8> {
  constructor(arg: number, heap: WasmHeap) {
    super(arg, heap, Uint8);
  }

  str(): string {
    return "TODO";
  }
}

export type u8 = Uint8;
export type voidp = Ptr<Void>;
export type voidp_arr = Ptr<Ptr<Void>>;
export type u32_arr = Ptr<Uint32>;
export type i32_arr = Ptr<Sint32>;
export type str_arr = Ptr<Ptr<Uint8>>;