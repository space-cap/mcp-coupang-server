"""
Coupang category codes and names.

쿠팡 카테고리 코드 및 이름 정의.
"""

# 쿠팡 카테고리 코드 매핑
CATEGORY_MAP = {
    "1001": "여성패션",
    "1002": "남성패션",
    "1010": "뷰티",
    "1012": "식품",
    "1013": "주방용품",
    "1014": "생활용품",
    "1015": "홈인테리어",
    "1016": "가전디지털",
    "1017": "스포츠/레저",
    "1018": "자동차용품",
    "1019": "도서/음반/DVD",
    "1020": "완구/취미",
    "1021": "문구/오피스",
    "1024": "헬스/건강식품",
    "1025": "국내여행",
    "1026": "해외여행",
    "1029": "반려동물용품",
    "1030": "유아동패션",
}


def get_category_name(category_id: str) -> str:
    """
    Get category name by category ID.

    Args:
        category_id: Coupang category ID

    Returns:
        Category name in Korean, or "Unknown" if not found

    Example:
        >>> get_category_name("1001")
        '여성패션'
    """
    return CATEGORY_MAP.get(category_id, "Unknown")


def get_all_categories() -> dict:
    """
    Get all available categories.

    Returns:
        Dictionary of category ID to name mappings

    Example:
        >>> categories = get_all_categories()
        >>> print(categories["1001"])
        '여성패션'
    """
    return CATEGORY_MAP.copy()


def is_valid_category(category_id: str) -> bool:
    """
    Check if category ID is valid.

    Args:
        category_id: Coupang category ID

    Returns:
        True if valid, False otherwise

    Example:
        >>> is_valid_category("1001")
        True
        >>> is_valid_category("9999")
        False
    """
    return category_id in CATEGORY_MAP


def get_category_list_text() -> str:
    """
    Get formatted category list as text.

    Returns:
        Formatted string with all categories

    Example:
        >>> print(get_category_list_text())
        1001 - 여성패션
        1002 - 남성패션
        ...
    """
    lines = []
    for category_id, name in sorted(CATEGORY_MAP.items()):
        lines.append(f"{category_id} - {name}")
    return "\n".join(lines)
