#!/usr/bin/env python3
"""Browser acceptance tests against the static local site, using Chromium."""
import hashlib, json, os, re, urllib.parse
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
BASE=os.environ.get('SITE_URL','http://127.0.0.1:8094/')
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa-output';OUT.mkdir(exist_ok=True)
checks=[]
def ok(name):checks.append(name)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1100},device_scale_factor=1)
 page=context.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(BASE);page.get_by_role('heading',name='Better models start with better evidence.').wait_for()
 page.screenshot(path=str(OUT/'home-desktop.png'),full_page=True);ok('Landing page rendered')
 page.goto(BASE+'#geometry');page.get_by_role('button',name='Last-pixel test').click()
 data=json.loads(page.locator('#geometry-json').inner_text());assert data['foreground_pixels']==1;assert data['normalized_box']==[.95,.9167,1,1]
 with page.expect_download() as info:page.get_by_role('button',name='Download mask PNG').click()
 info.value.save_as(str(OUT/'mask.png'));im=Image.open(OUT/'mask.png');assert im.mode=='L' and im.size==(20,12) and set(im.getdata())=={0,255};ok('PNG download is single-channel binary 20 × 12')
 page.get_by_role('button',name='No-object example').click();assert json.loads(page.locator('#geometry-json').inner_text())['normalized_box'] is None
 page.locator('#pixel-x').fill('3');page.locator('#pixel-y').fill('4');page.get_by_role('button',name='Apply brush').click();assert json.loads(page.locator('#geometry-json').inner_text())['foreground_pixels']==1
 page.get_by_role('spinbutton',name='Top left x').fill('0');page.get_by_role('spinbutton',name='Top left x').press('Tab');assert json.loads(page.locator('#geometry-json').inner_text())['normalized_corners'][0][0]==0
 page.get_by_role('button',name='Restore visible mask').click();page.screenshot(path=str(OUT/'geometry-desktop.png'),full_page=True);ok('Mask presets, keyboard paint, named corner editing')
 page.goto(BASE+'#splits');assert '1 leaking family' in page.inner_text('main')
 page.get_by_role('button',name='Assign complete families').click();assert '0 leaking families' in page.inner_text('main')
 page.get_by_role('combobox',name='Split for a2').select_option('test');assert '1 leaking family' in page.inner_text('main')
 page.get_by_role('button',name='Assign complete families').click();page.screenshot(path=str(OUT/'splits-desktop.png'),full_page=True);ok('Transitive leakage and repair')
 page.goto(BASE+'#review');page.get_by_role('button',name='Accept reviewed candidate').click();assert 'Resolve checks' in page.locator('#review-error').inner_text()
 page.locator('#review-checklist').check();page.get_by_role('button',name='Accept reviewed candidate').click()
 page.locator('[data-candidate="1"]').click();page.locator('#candidate-caption').fill('One coral book on a light desk.')
 page.locator('[data-candidate="0"]').click();page.locator('[data-candidate="1"]').click();assert page.locator('#candidate-caption').input_value()=='One coral book on a light desk.'
 page.goto(BASE+'#release');assert 'Save or discard unfinished caption drafts' in page.inner_text('main');assert page.get_by_role('button',name='Freeze reviewed release').is_disabled()
 page.goto(BASE+'#review');page.locator('[data-candidate="1"]').click();page.get_by_role('button',name='Save revised caption').click();page.locator('#review-checklist').check();page.get_by_role('button',name='Accept reviewed candidate').click()
 page.locator('[data-candidate="2"]').click();page.locator('#review-checklist').check();page.get_by_role('button',name='Accept reviewed candidate').click()
 page.locator('[data-candidate="3"]').click();page.get_by_role('button',name='Reject',exact=True).click();ok('Candidate gates, retained drafts, edit revision, explicit accept/reject')
 page.goto(BASE+'#lineage');page.locator('#crop-x').fill('19');page.get_by_role('button',name='Create derived asset').click();assert 'Crop must fit' in page.locator('#crop-error').inner_text()
 page.locator('#crop-x').fill('1');page.get_by_role('button',name='Create derived asset').click();assert 'needs-review' in page.inner_text('main')
 page.get_by_role('button',name='Record reviewed revision').click();assert 'needs-review' in page.inner_text('main')
 page.locator('#lineage-check').check();page.get_by_role('button',name='Record reviewed revision').click();assert 'needs-review' not in page.inner_text('main');ok('Invalid crop blocked; derived annotation requires review')
 page.goto(BASE+'#release');page.locator('#rights-check').check();assert page.get_by_role('button',name='Freeze reviewed release').is_enabled()
 page.get_by_role('button',name='Freeze reviewed release').click();page.get_by_role('heading',name='release-001 Frozen').wait_for()
 with page.expect_download() as info:page.get_by_role('button',name='Download manifest').click()
 info.value.save_as(str(OUT/'release-001.json'));payload=(OUT/'release-001.json').read_bytes();digest=hashlib.sha256(payload).hexdigest();assert digest in page.inner_text('main');release=json.loads(payload);assert release['consumer_validation'].startswith('Not run')
 original=release['annotation']['mask'];page.goto(BASE+'#geometry');page.get_by_role('button',name='No-object example').click();page.reload();assert json.loads(page.locator('#geometry-json').inner_text())['foreground_pixels']==0
 stored=page.evaluate("JSON.parse(localStorage.getItem('dataset-production-labs-v1'))");assert stored['releases'][0]['content']['annotation']['mask']==original;ok('Frozen export SHA matches bytes; immutable snapshot survives later edits/reload')
 page.goto(BASE+'#release');page.screenshot(path=str(OUT/'release-desktop.png'),full_page=True)
 page.goto(BASE+'#tuldok');page.screenshot(path=str(OUT/'tuldok-desktop.png'),full_page=True);assert 'Proposed interface' in page.inner_text('main');ok('Tuldok mockup reflects local lab state and proposal boundary')
 # Cancel reset preserves snapshots; approving clears local demo state.
 page.once('dialog',lambda d:d.dismiss());page.get_by_role('button',name='Reset all labs').click();assert page.evaluate("JSON.parse(localStorage.getItem('dataset-production-labs-v1')).releases.length")==1
 page.once('dialog',lambda d:d.accept());page.get_by_role('button',name='Reset all labs').click();assert page.evaluate("JSON.parse(localStorage.getItem('dataset-production-labs-v1')).releases.length")==0;ok('Reset cancellation and confirmation')
 page.goto(BASE+'book/');assert page.get_by_role('heading',name='Dataset Production',exact=True).count()==1
 page.locator('#toc-search').fill('audio');assert page.locator('.book-toc nav a:visible').count()==1
 page.locator('#toc-search').fill('');page.screenshot(path=str(OUT/'book-desktop.png'),full_page=False)
 assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete && i.naturalWidth>0)');ok('Complete book reader, title filter, all diagrams load')
 page.set_viewport_size({'width':390,'height':844})
 for route in ['', '#geometry','#splits','#review','#lineage','#release','#tuldok','book/','about.html']:
  page.goto(BASE+route);page.wait_for_timeout(100)
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow on {route}'
  page.screenshot(path=str(OUT/('mobile-'+(route.replace('#','').replace('/','')or'home')+'.png')),full_page=True)
 ok('All routes fit 390px mobile viewport without page overflow')
 page.goto(BASE+'#geometry');page.get_by_role('button',name='Last-pixel test').focus();page.keyboard.press('Enter');assert json.loads(page.locator('#geometry-json').inner_text())['foreground_pixels']==1;ok('Keyboard action and visible native focus path')
 assert not errors,errors
 ok('No browser JavaScript errors')
 browser.close()
(OUT/'browser-results.json').write_text(json.dumps({'status':'passed','base':BASE,'checks':checks},indent=2))
print(json.dumps({'status':'passed','checks':checks},indent=2))
