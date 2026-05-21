import ezdxf
import numpy as np
import os
from shapely import concave_hull
from shapely.geometry import MultiPoint, Polygon, MultiPolygon


def calculate_dxf_area(
    filepath: str,
    ignore_layers=None,
    zero_tol: float = 1e-6,
    axis_zero_tol: float = 1e-3,
    axis_far_threshold: float = 1000.0,
    iqr_k: float = 2.5,
    max_hull_points: int = 15000,
):
    try:
        ignore_layers = {str(x).lower() for x in (ignore_layers or set())}

        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()

        points = []

        for entity in msp:
            layer = str(getattr(entity.dxf, "layer", "0")).lower()
            if ignore_layers and any(mask in layer for mask in ignore_layers):
                continue

            dxftype = entity.dxftype()

            if dxftype == "LWPOLYLINE":
                for x, y in entity.vertices():
                    points.append((float(x), float(y)))

            elif dxftype == "POLYLINE":
                for v in entity.points():
                    points.append((float(v[0]), float(v[1])))

            elif dxftype == "LINE":
                points.append((float(entity.dxf.start.x), float(entity.dxf.start.y)))
                points.append((float(entity.dxf.end.x), float(entity.dxf.end.y)))

            elif dxftype in ("TEXT", "MTEXT", "INSERT") and hasattr(entity.dxf, "insert"):
                points.append((float(entity.dxf.insert.x), float(entity.dxf.insert.y)))

        if len(points) < 4:
            return filepath, 0.0

        points_array = np.asarray(points, dtype=np.float64)
        points_array = points_array[np.isfinite(points_array).all(axis=1)]

        if len(points_array) < 4:
            return filepath, 0.0

        points_array = np.round(points_array, 3)
        points_array = np.unique(points_array, axis=0)

        if len(points_array) < 4:
            return filepath, 0.0

        # Exclude (0, 0)
        points_array = points_array[
            ~(
                (np.abs(points_array[:, 0]) <= zero_tol) &
                (np.abs(points_array[:, 1]) <= zero_tol)
            )
        ]

        if len(points_array) < 4:
            return filepath, 0.0

        # Если чертёж далеко от нуля — убираем точки на осях
        if np.median(np.abs(points_array[:, 0])) > axis_far_threshold:
            points_array = points_array[np.abs(points_array[:, 0]) > axis_zero_tol]

        if np.median(np.abs(points_array[:, 1])) > axis_far_threshold:
            points_array = points_array[np.abs(points_array[:, 1]) > axis_zero_tol]

        if len(points_array) < 4:
            return filepath, 0.0

        # IQR-фильтр выбросов
        q1_x, q3_x = np.percentile(points_array[:, 0], [25, 75])
        q1_y, q3_y = np.percentile(points_array[:, 1], [25, 75])

        iqr_x = q3_x - q1_x
        iqr_y = q3_y - q1_y

        x_min = q1_x - iqr_k * iqr_x if iqr_x > 0 else points_array[:, 0].min()
        x_max = q3_x + iqr_k * iqr_x if iqr_x > 0 else points_array[:, 0].max()
        y_min = q1_y - iqr_k * iqr_y if iqr_y > 0 else points_array[:, 1].min()
        y_max = q3_y + iqr_k * iqr_y if iqr_y > 0 else points_array[:, 1].max()

        filtered_points = points_array[
            (points_array[:, 0] >= x_min) & (points_array[:, 0] <= x_max) &
            (points_array[:, 1] >= y_min) & (points_array[:, 1] <= y_max)
        ]

        if len(filtered_points) < 4:
            return filepath, 0.0

        filtered_points = np.unique(filtered_points, axis=0)

        if len(filtered_points) > max_hull_points:
            step = max(1, len(filtered_points) // max_hull_points)
            filtered_points = filtered_points[::step]

        boundary = concave_hull(
            MultiPoint(filtered_points),
            ratio=0.15,
            allow_holes=False,
        )

        if boundary.is_empty:
            return filepath, 0.0

        if isinstance(boundary, Polygon):
            return filepath, float(boundary.area)

        elif isinstance(boundary, MultiPolygon):
            total_area = float(sum(poly.area for poly in boundary.geoms if not poly.is_empty))
            return filepath, total_area

        return filepath, 0.0

    except Exception as e:
        return filepath, f"Error: {e}"


def calculate_dxf_area_and_save_contour(
    filepath: str,
    ignore_layers=None,
    zero_tol: float = 1e-6,
    axis_zero_tol: float = 1e-3,
    axis_far_threshold: float = 1000.0,
    iqr_k: float = 2.5,
    max_hull_points: int = 15000,
):
    try:
        ignore_layers = {str(x).lower() for x in (ignore_layers or set())}

        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()

        points = []

        for entity in msp:
            layer = str(getattr(entity.dxf, "layer", "0")).lower()
            if ignore_layers and any(mask in layer for mask in ignore_layers):
                continue

            dxftype = entity.dxftype()

            if dxftype == "LWPOLYLINE":
                for x, y in entity.vertices():
                    points.append((float(x), float(y)))

            elif dxftype == "POLYLINE":
                for v in entity.points():
                    points.append((float(v[0]), float(v[1])))

            elif dxftype == "LINE":
                points.append((float(entity.dxf.start.x), float(entity.dxf.start.y)))
                points.append((float(entity.dxf.end.x), float(entity.dxf.end.y)))

            elif dxftype in ("TEXT", "MTEXT", "INSERT") and hasattr(entity.dxf, "insert"):
                points.append((float(entity.dxf.insert.x), float(entity.dxf.insert.y)))

        if len(points) < 4:
            return filepath, 0.0

        points_array = np.asarray(points, dtype=np.float64)
        points_array = points_array[np.isfinite(points_array).all(axis=1)]

        if len(points_array) < 4:
            return filepath, 0.0

        points_array = np.round(points_array, 3)
        points_array = np.unique(points_array, axis=0)

        if len(points_array) < 4:
            return filepath, 0.0

        # Убираем (0, 0)
        points_array = points_array[
            ~(
                (np.abs(points_array[:, 0]) <= zero_tol) &
                (np.abs(points_array[:, 1]) <= zero_tol)
            )
        ]

        if len(points_array) < 4:
            return filepath, 0.0

        # Если чертёж далеко от нуля — убираем точки на осях
        if np.median(np.abs(points_array[:, 0])) > axis_far_threshold:
            points_array = points_array[np.abs(points_array[:, 0]) > axis_zero_tol]

        if np.median(np.abs(points_array[:, 1])) > axis_far_threshold:
            points_array = points_array[np.abs(points_array[:, 1]) > axis_zero_tol]

        if len(points_array) < 4:
            return filepath, 0.0

        # IQR-фильтр выбросов
        q1_x, q3_x = np.percentile(points_array[:, 0], [25, 75])
        q1_y, q3_y = np.percentile(points_array[:, 1], [25, 75])

        iqr_x = q3_x - q1_x
        iqr_y = q3_y - q1_y

        x_min = q1_x - iqr_k * iqr_x if iqr_x > 0 else points_array[:, 0].min()
        x_max = q3_x + iqr_k * iqr_x if iqr_x > 0 else points_array[:, 0].max()
        y_min = q1_y - iqr_k * iqr_y if iqr_y > 0 else points_array[:, 1].min()
        y_max = q3_y + iqr_k * iqr_y if iqr_y > 0 else points_array[:, 1].max()

        filtered_points = points_array[
            (points_array[:, 0] >= x_min) & (points_array[:, 0] <= x_max) &
            (points_array[:, 1] >= y_min) & (points_array[:, 1] <= y_max)
        ]

        if len(filtered_points) < 4:
            return filepath, 0.0

        # Ограничиваем число точек перед hull
        filtered_points = np.unique(filtered_points, axis=0)

        if len(filtered_points) > max_hull_points:
            step = max(1, len(filtered_points) // max_hull_points)
            filtered_points = filtered_points[::step]

        boundary = concave_hull(
            MultiPoint(filtered_points),
            ratio=0.15,
            allow_holes=False,
        )

        if boundary.is_empty:
            return filepath, 0.0

        if isinstance(boundary, Polygon):
            polygons = [boundary]
        elif isinstance(boundary, MultiPolygon):
            polygons = [poly for poly in boundary.geoms if not poly.is_empty]
        else:
            return filepath, 0.0

        if not polygons:
            return filepath, 0.0

        contour_layer = "_AREA_CONTOUR"
        if contour_layer not in doc.layers:
            doc.layers.add(name=contour_layer, color=1)

        saved_any = False

        for poly in polygons:
            coords = [(float(x), float(y)) for x, y in list(poly.exterior.coords)[:-1]]

            if len(coords) < 3:
                continue

            if doc.dxfversion == "AC1009":
                msp.add_polyline2d(coords, close=True, dxfattribs={"layer": contour_layer, "color": 1})
            else:
                msp.add_lwpolyline(coords, close=True, dxfattribs={"layer": contour_layer, "color": 1})

            saved_any = True

        if not saved_any:
            return filepath, 0.0

        new_path = os.path.join(os.path.dirname(filepath), f"0_lines_{os.path.basename(filepath)}")
        doc.saveas(new_path)

        total_area = float(sum(poly.area for poly in polygons))
        return new_path, total_area

    except Exception as e:
        return filepath, f"Error: {e}"