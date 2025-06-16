function test(u) {
  return function (n, r, t) {
    r = n.B(0);
    t = n.B(1);
    return u(r, t);
  };
}