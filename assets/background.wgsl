fn gaanim_background(uv: vec2<f32>, resolution: vec2<f32>, time: f32) -> vec4<f32> {
    let p = uv - vec2<f32>(0.5);
    let aspect = resolution.x / resolution.y;
    let q = vec2<f32>(p.x * aspect, p.y);

    let paper = vec3<f32>(0.974, 0.978, 0.986);
    let blueprint = vec3<f32>(0.100, 0.065, 0.420);
    let title_blue = vec3<f32>(0.150, 0.105, 0.700);

    let wave_y = q.y
        + 0.040 * sin(q.x * 4.6 - time * 0.10)
        + 0.014 * sin(q.x * 10.0 + time * 0.065);
    let contour_phase = abs(fract((wave_y - 0.28) * 22.0) - 0.5);
    let contours = 1.0 - smoothstep(0.010, 0.032, contour_phase);
    let lower_zone = 1.0 - smoothstep(-0.47, -0.25, q.y);
    let wash = lower_zone * (0.048 + 0.014 * sin(q.x * 2.2 - time * 0.05));
    let contour_ink = contours * lower_zone * 0.046;

    let color = mix(paper, title_blue, wash);
    let final_color = mix(color, blueprint, contour_ink);
    return vec4<f32>(final_color, 1.0);
}
