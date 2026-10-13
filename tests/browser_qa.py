#!/usr/bin/env python3
"""Qualify checkout bytes in sandboxed Chromium; screenshots need visual review.

Use a loopback server, never production. No insecure launch flags or fallback.
The receipt is written even on missing dependencies, launch or assertion failure.
"""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import traceback
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qa-output'
BASE = os.environ.get('SITE_URL', 'http://127.0.0.1:8094/').rstrip('/') + '/'
checks, errors, resource_errors, screenshots = [], [], [], []
receipt = {
    'status': 'running', 'base': BASE, 'checks': checks,
    'commit': os.environ.get('BOOK_QA_COMMIT', 'local-uncommitted-candidate'),
    'browser': 'Playwright bundled Chromium', 'chromium_sandbox': True,
    'screenshots': screenshots, 'javascript_errors': errors,
    'resource_errors': resource_errors,
    'visual_review': 'Required: inspect screenshots for clipping, overlap, readable figures and focus visibility. No pixel-baseline comparison is performed.',
    'limits': ['Linux Chromium only; narrow viewports are not physical mobile-device tests.',
               'No Safari/Firefox, screen-reader, GPU/model or production deployment qualification.',
               'PDF page layout requires separate visual evidence.'],
}


def write_receipt():
    OUT.mkdir(exist_ok=True)
    (OUT / 'browser-results.json').write_text(json.dumps(receipt, indent=2) + '\n')


def ok(name):
    checks.append(name)
    write_receipt()
    print('Passed: ' + name, flush=True)


def capture(page, name, full_page=False):
    page.screenshot(path=str(OUT / (name + '.png')), full_page=full_page)
    screenshots.append(name + '.png')


def observe_page(page):
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda message: errors.append('console.error: ' + message.text) if message.type == 'error' else None)
    page.on('response', lambda response: resource_errors.append({'url': response.url, 'status': response.status}) if response.status >= 400 else None)
    page.on('requestfailed', lambda request: resource_errors.append({'url': request.url, 'failure': request.failure}))


def restrict_to_loopback(context):
    origin = urlsplit(BASE).netloc
    context.route('**/*', lambda route: route.continue_() if urlsplit(route.request.url).netloc == origin or urlsplit(route.request.url).scheme in ('data', 'blob') else route.abort())
    context.on('page', observe_page)


def ready(page):
    page.evaluate('document.fonts.ready')
    page.wait_for_function('Array.from(document.images).every(i => i.complete)')
    assert page.locator('img').evaluate_all('(images) => images.every(i => i.naturalWidth > 0)'), 'Image failed to decode'


def visit(page, route=''):
    response = page.goto(BASE + route, wait_until='networkidle')
    if response is not None:
        assert response.ok, (route, response.status)
    ready(page)


def no_overflow(page, label):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), label


def reader_checks(browser, page, expect):
    page.set_viewport_size({'width': 1440, 'height': 1000})
    visit(page, 'book/')
    expect(page.get_by_role('heading', name='Dataset Production', exact=True)).to_have_count(1)
    expect(page.locator('article h1[id^="chapter-"]')).to_have_count(15)
    expect(page.locator('article h1[id^="part-"]')).to_have_count(4)
    expect(page.locator('article h1[id^="track-0"]')).to_have_count(6)
    expect(page.locator('article h1[id^="appendix-"]')).to_have_count(4)
    expect(page.locator('.book-edition')).to_contain_text('15 core chapters')
    expect(page.locator('.book-edition')).to_contain_text('6 optional tracks')
    capture(page, 'book-desktop-opening')
    ok('Reader: 15 core chapters, four parts, six modality tracks, four appendices; all images decode')

    search = page.get_by_role('searchbox', name='Find a chapter')
    search.fill('audio')
    expect(page.locator('.book-toc nav a:visible')).to_have_count(1)
    page.locator('.book-toc nav a:visible').focus()
    page.keyboard.press('Enter')
    expect(page).to_have_url(BASE + 'book/#track-04-audio')
    page.go_back()
    expect(page).to_have_url(BASE + 'book/')
    page.go_forward()
    expect(page).to_have_url(BASE + 'book/#track-04-audio')
    search.fill('no chapter matches this')
    expect(page.locator('.book-toc nav a:visible')).to_have_count(0)
    expect(page.locator('#toc-result')).to_have_text('0 matching sections')
    search.fill('')
    assert page.locator('.book-toc nav a:visible').count() > 25
    ok('Reader filter, zero-result recovery, keyboard anchor activation, browser back and forward')

    anchors = ['book-title', 'chapter-inspect-release', 'chapter-data-contract',
               'chapter-audit-baseline', 'chapter-freeze-consumer',
               'chapter-operate-recover-cost', 'track-03-vision-video',
               'track-06-physical-fields-simulation', 'case-01-rheon', 'case-02-tuldok']
    for width, height, label in [(1440, 1000, 'desktop'), (390, 844, 'mobile'), (320, 740, 'small-phone')]:
        page.set_viewport_size({'width': width, 'height': height})
        for anchor in anchors:
            visit(page, 'book/#' + anchor)
            expect(page.locator('#' + anchor)).to_be_in_viewport()
            no_overflow(page, (width, anchor))
            capture(page, 'reader-' + label + '-' + anchor)
        regions = page.locator('article pre')
        assert regions.count() > 0
        for region in regions.all():
            assert region.get_attribute('tabindex') == '0'
            assert region.evaluate('(el) => getComputedStyle(el).whiteSpace') == 'pre'
            assert region.evaluate('(el) => getComputedStyle(el).overflowX') == 'auto'
        widest = regions.evaluate_all('(els) => els.reduce((best, el, i) => el.scrollWidth-el.clientWidth > best.amount ? {index:i, amount:el.scrollWidth-el.clientWidth} : best, {index:0, amount:0})')
        region = regions.nth(widest['index'])
        region.scroll_into_view_if_needed()
        # Keyboard Tab, rather than pointer input, establishes :focus-visible.
        region.focus()
        page.keyboard.press('Tab')
        region.focus()
        assert region.evaluate('(el) => document.activeElement === el')
        assert region.evaluate('(el) => el.matches(":focus-visible")')
        assert region.evaluate('(el) => getComputedStyle(el).outlineStyle') != 'none'
        if width <= 390:
            assert widest['amount'] > 0, 'No real overflow region available for keyboard-scroll qualification'
            region.evaluate('(el) => { el.scrollLeft = 0; }')
            page.keyboard.press('ArrowRight')
            page.wait_for_function('(index) => document.querySelectorAll("article pre")[index].scrollLeft > 0', arg=widest['index'])
        no_overflow(page, (width, 'keyboard-scroll'))
        capture(page, 'reader-' + label + '-keyboard-scroller')
    ok('1440/390/320px reader fits; rows preserved; visible keyboard focus and real horizontal scrolling')

    visit(page, 'research-edition/')
    expect(page.get_by_role('heading', name='Dataset Production', exact=True)).to_have_count(1)
    expect(page.locator('.book-edition')).to_contain_text('16 chapters')
    no_overflow(page, 'research-edition')
    capture(page, 'research-edition-small-phone')
    ok('Preserved research edition loads independently')

    # Disable JS before navigation, not by removing a script after execution.
    static_context = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    static = None
    try:
        restrict_to_loopback(static_context)
        static = static_context.new_page()
        response = static.goto(BASE + 'book/', wait_until='load')
        assert response.ok
        expect(static.locator('article h1[id^="chapter-"]')).to_have_count(15)
        static.locator('.book-toc nav a[href="#track-04-audio"]').click()
        expect(static).to_have_url(BASE + 'book/#track-04-audio')
        expect(static.locator('#track-04-audio')).to_be_in_viewport()
        capture(static, 'reader-no-javascript-mobile')
    except Exception:
        if static is not None:
            receipt['failure_url'] = static.url
            receipt['failure_context'] = 'javascript-disabled reader'
            try:
                capture(static, 'failure-no-javascript')
            except Exception as screenshot_error:
                receipt['failure_screenshot_error'] = str(screenshot_error)
        raise
    finally:
        static_context.close()
    ok('Fresh no-JavaScript context: reader text and anchor navigation work')


def lab_checks(page, expect, Image):
    visit(page)
    page.get_by_role('heading', name='Better models start with better evidence.').wait_for()
    expect(page.locator('.meta-row')).to_contain_text('Principles-first edition / 13 Oct 2026')
    capture(page, 'home-desktop', full_page=True)
    ok('Landing page rendered')
    visit(page, '#geometry')
    page.get_by_role('button', name='Last-pixel test').click()
    data = json.loads(page.locator('#geometry-json').inner_text())
    assert data['foreground_pixels'] == 1
    assert data['normalized_box'] == [0.95, 0.9167, 1, 1]
    with page.expect_download() as info:
        page.get_by_role('button', name='Download mask PNG').click()
    info.value.save_as(str(OUT / 'mask.png'))
    im = Image.open(OUT / 'mask.png')
    assert im.mode == 'L' and im.size == (20, 12) and (set(im.getdata()) == {0, 255})
    ok('PNG download is single-channel binary 20 × 12')
    page.get_by_role('button', name='No-object example').click()
    assert json.loads(page.locator('#geometry-json').inner_text())['normalized_box'] is None
    page.locator('#pixel-x').fill('3')
    page.locator('#pixel-y').fill('4')
    page.get_by_role('button', name='Apply brush').click()
    assert json.loads(page.locator('#geometry-json').inner_text())['foreground_pixels'] == 1
    page.get_by_role('spinbutton', name='Top left x').fill('0')
    page.get_by_role('spinbutton', name='Top left x').press('Tab')
    assert json.loads(page.locator('#geometry-json').inner_text())['normalized_corners'][0][0] == 0
    page.get_by_role('button', name='Restore visible mask').click()
    capture(page, 'geometry-desktop', full_page=True)
    ok('Mask presets, keyboard paint, named corner editing')
    visit(page, '#splits')
    assert '1 leaking family' in page.inner_text('main')
    page.get_by_role('button', name='Assign complete families').click()
    assert '0 leaking families' in page.inner_text('main')
    page.get_by_role('combobox', name='Split for a2').select_option('test')
    assert '1 leaking family' in page.inner_text('main')
    page.get_by_role('button', name='Assign complete families').click()
    capture(page, 'splits-desktop', full_page=True)
    ok('Transitive leakage and repair')
    visit(page, '#review')
    page.get_by_role('button', name='Accept reviewed candidate').click()
    assert 'Resolve checks' in page.locator('#review-error').inner_text()
    page.locator('#review-checklist').check()
    page.get_by_role('button', name='Accept reviewed candidate').click()
    page.locator('[data-candidate="1"]').click()
    page.locator('#candidate-caption').fill('One coral book on a light desk.')
    page.locator('[data-candidate="0"]').click()
    page.locator('[data-candidate="1"]').click()
    assert page.locator('#candidate-caption').input_value() == 'One coral book on a light desk.'
    visit(page, '#release')
    assert 'Save or discard unfinished caption drafts' in page.inner_text('main')
    assert page.get_by_role('button', name='Freeze reviewed release').is_disabled()
    visit(page, '#review')
    page.locator('[data-candidate="1"]').click()
    page.get_by_role('button', name='Save revised caption').click()
    page.locator('#review-checklist').check()
    page.get_by_role('button', name='Accept reviewed candidate').click()
    page.locator('[data-candidate="2"]').click()
    page.locator('#review-checklist').check()
    page.get_by_role('button', name='Accept reviewed candidate').click()
    page.locator('[data-candidate="3"]').click()
    page.get_by_role('button', name='Reject', exact=True).click()
    ok('Candidate gates, retained drafts, edit revision, explicit accept/reject')
    visit(page, '#lineage')
    page.locator('#crop-x').fill('19')
    page.get_by_role('button', name='Create derived asset').click()
    assert 'Crop must fit' in page.locator('#crop-error').inner_text()
    page.locator('#crop-x').fill('1')
    page.get_by_role('button', name='Create derived asset').click()
    assert 'needs-review' in page.inner_text('main')
    page.get_by_role('button', name='Record reviewed revision').click()
    assert 'needs-review' in page.inner_text('main')
    page.locator('#lineage-check').check()
    page.get_by_role('button', name='Record reviewed revision').click()
    assert 'needs-review' not in page.inner_text('main')
    ok('Invalid crop blocked; derived annotation requires review')
    visit(page, '#release')
    page.locator('#rights-check').check()
    assert page.get_by_role('button', name='Freeze reviewed release').is_enabled()
    page.get_by_role('button', name='Freeze reviewed release').click()
    page.get_by_role('heading', name='release-001 Frozen').wait_for()
    with page.expect_download() as info:
        page.get_by_role('button', name='Download manifest').click()
    info.value.save_as(str(OUT / 'release-001.json'))
    payload = (OUT / 'release-001.json').read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    assert digest in page.inner_text('main')
    release = json.loads(payload)
    assert release['consumer_validation'].startswith('Not run')
    original = release['annotation']['mask']
    visit(page, '#geometry')
    page.get_by_role('button', name='No-object example').click()
    page.reload()
    assert json.loads(page.locator('#geometry-json').inner_text())['foreground_pixels'] == 0
    stored = page.evaluate("JSON.parse(localStorage.getItem('dataset-production-labs-v1'))")
    assert stored['releases'][0]['content']['annotation']['mask'] == original
    ok('Frozen export SHA matches bytes; immutable snapshot survives later edits/reload')
    visit(page, '#release')
    capture(page, 'release-desktop', full_page=True)
    visit(page, '#tuldok')
    capture(page, 'tuldok-desktop', full_page=True)
    assert 'Proposed interface' in page.inner_text('main')
    ok('Tuldok mockup reflects local lab state and proposal boundary')
    # Cancelling reset must preserve every saved byte, not only the snapshot count.
    before_reset = page.evaluate("localStorage.getItem('dataset-production-labs-v1')")
    page.once('dialog', lambda d: d.dismiss())
    page.get_by_role('button', name='Reset all labs').click()
    assert page.evaluate("JSON.parse(localStorage.getItem('dataset-production-labs-v1')).releases.length") == 1
    assert page.evaluate("localStorage.getItem('dataset-production-labs-v1')") == before_reset
    capture(page, 'reset-cancelled-preserved-release')
    page.once('dialog', lambda d: d.accept())
    page.get_by_role('button', name='Reset all labs').click()
    assert page.evaluate("JSON.parse(localStorage.getItem('dataset-production-labs-v1')).releases.length") == 0
    capture(page, 'reset-confirmed-cleared-release')
    ok('Reset cancellation preserves exact saved state; confirmation clears snapshots')
    for width, height, label in [(1440, 1000, 'desktop'), (390, 844, 'mobile'), (320, 740, 'small-phone')]:
        page.set_viewport_size({'width': width, 'height': height})
        for route in ['', '#geometry', '#splits', '#review', '#lineage', '#release', '#tuldok', 'book/', 'research-edition/', 'about.html']:
            visit(page, route)
            no_overflow(page, (width, route))
            name = route.replace('#', '').replace('/', '') or 'home'
            capture(page, label + '-' + name, full_page=route not in ('book/', 'research-edition/'))
    ok('Landing, all six labs, both readers and About fit actual 1440/390/320px layouts')
    visit(page, '#geometry')
    page.get_by_role('button', name='Last-pixel test').focus()
    page.keyboard.press('Enter')
    assert json.loads(page.locator('#geometry-json').inner_text())['foreground_pixels'] == 1
    assert page.get_by_role('button', name='Last-pixel test').evaluate('(el) => el.matches(":focus-visible")')
    capture(page, 'lab-small-phone-keyboard-focus')
    ok('Lab keyboard action and visible focus')
    page.locator('.lab-nav a[href="#splits"]').click()
    expect(page).to_have_url(BASE + '#splits')
    expect(page.get_by_role('button', name='Assign complete families')).to_be_visible()
    page.go_back()
    expect(page).to_have_url(BASE + '#geometry')
    expect(page.locator('#geometry-json')).to_contain_text('foreground_pixels')
    assert json.loads(page.locator('#geometry-json').inner_text())['foreground_pixels'] == 1
    page.go_forward()
    expect(page).to_have_url(BASE + '#splits')
    expect(page.get_by_role('button', name='Assign complete families')).to_be_visible()
    ok('Lab back/forward restores route and retains edited annotation')


def run():
    page = context = browser = None
    write_receipt()
    try:
        from PIL import Image
        from playwright.sync_api import expect, sync_playwright
        parsed = urlsplit(BASE)
        assert parsed.scheme == 'http' and parsed.hostname in ('127.0.0.1', 'localhost', '::1'), 'Use only a loopback server serving this checkout'
        assert not parsed.username and not parsed.password and not parsed.query and not parsed.fragment
        receipt['playwright_version'] = importlib.metadata.version('playwright')
        files = {path.relative_to(ROOT / 'docs').as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                 for path in sorted((ROOT / 'docs').rglob('*')) if path.is_file()}
        receipt['docs_tree_sha256'] = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
        receipt['manuscript_sha256'] = files['book/manuscript.md']
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True, channel='chromium', chromium_sandbox=True)
                receipt['browser_version'] = browser.version
                context = browser.new_context(viewport={'width': 1440, 'height': 1100}, device_scale_factor=1,
                                              reduced_motion='reduce', accept_downloads=True)
                context.tracing.start(screenshots=True, snapshots=True, sources=True)
                restrict_to_loopback(context)
                page = context.new_page()
                for name in ['index.html', 'book/index.html', 'book/reader.js', 'style.css', 'app.js', 'core.js', 'book/manuscript.md']:
                    response = context.request.get(BASE + name)
                    assert response.ok and hashlib.sha256(response.body()).hexdigest() == files[name], 'Served bytes differ: ' + name
                ok('Loopback reader, labs, manuscript and stylesheet match exact checked-out bytes')
                lab_checks(page, expect, Image)
                reader_checks(browser, page, expect)
                assert not errors, errors
                assert not resource_errors, resource_errors
                ok('No JavaScript exceptions, failed resources or HTTP errors in tested routes')
                receipt['status'] = 'passed'
            except Exception:
                if page is not None:
                    receipt.setdefault('failure_url', page.url)
                    try:
                        capture(page, 'failure-last-main-page' if 'failure_context' in receipt else 'failure')
                    except Exception as screenshot_error:
                        receipt['failure_screenshot_error'] = str(screenshot_error)
                raise
            finally:
                if context is not None:
                    try:
                        context.tracing.stop(path=str(OUT / 'browser-trace.zip'))
                    except Exception as trace_error:
                        receipt['trace_error'] = str(trace_error)
                    context.close()
                if browser is not None:
                    browser.close()
    except Exception as error:
        receipt['status'] = 'failed'
        receipt['error'] = str(error)
        receipt['traceback'] = traceback.format_exc()
        return_code = 1
    else:
        return_code = 0
    finally:
        write_receipt()
        print(json.dumps(receipt, indent=2), flush=True)
    return return_code


if __name__ == '__main__':
    sys.exit(run())
